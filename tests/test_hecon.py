"""Tests for the hecon package and refcheck. Each property is checked by running the code.
© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later"""
import http.server, json, os, sys, threading, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "tools"))
from hecon import model, game, health, economics
import refcheck

class Model(unittest.TestCase):
    def test_runs_and_is_deterministic(self):
        self.assertEqual(json.dumps(model.simulate()), json.dumps(model.simulate()))
    def test_ai_without_validity_or_capture_adds_no_competence(self):  # Proposition 2
        r = model.simulate({"validity": 0.0, "capture": 0.0})
        self.assertEqual(r["arms"]["harvest"]["competent"], r["arms"]["comparator"]["competent"])
    def test_validity_raises_competence(self):
        lo, hi = model.simulate({"validity": 0.2}), model.simulate({"validity": 1.0})
        self.assertGreater(sum(hi["arms"]["harvest"]["competent"]), sum(lo["arms"]["harvest"]["competent"]))
    def test_cultivation_grows_shared_infrastructure(self):
        r = model.simulate(); self.assertGreater(r["arms"]["cultivate"]["D"][-1], r["arms"]["harvest"]["D"][-1])
    def test_icer_quadrants(self):
        self.assertEqual(model.icer(-5, 2)["label"], "dominant"); self.assertEqual(model.icer(5, -1)["label"], "dominated")
        self.assertEqual(model.icer(10, 2)["value"], 5.0)
    def test_economics(self):
        s = economics.psa(n=20); self.assertEqual(len(s), 20)
        self.assertTrue(all(0.0 <= p <= 1.0 for _, p in economics.ceac(s, [0, 1000, 10000])))

class Game(unittest.TestCase):
    def test_defaults_have_two_equilibria_and_underprovision(self):
        self.assertEqual(game.equilibria(), [0, 3]); self.assertEqual(game.optimum(), 8)
    def test_recognition_makes_cultivation_dominant(self):
        self.assertEqual(game.equilibria({"r": 4}), [8])
    def test_replicator_stays_in_unit_interval(self):
        xs = game.replicator(0.5); self.assertTrue(all(0.0 <= x <= 1.0 for x in xs))

class Health(unittest.TestCase):
    def test_checksums(self):
        self.assertTrue(health.nhs_valid("999 000 0018")); self.assertTrue(health.nhs_valid("9434765919")); self.assertFalse(health.nhs_valid("9434765918"))
        self.assertTrue(health.verhoeff_valid("2363")); self.assertFalse(health.verhoeff_valid("2364"))
    def test_deidentification_removes_every_identifier_and_keeps_clinical_values(self):
        clean, rep = health.deidentify(health.CASE_TEXT, names=health.CASE_NAMES)
        ev = health.evaluate(clean, health.GOLD_IDENTIFIERS, health.CLINICAL_VALUES)
        self.assertEqual(ev["missed"], []); self.assertEqual(ev["lost"], [])
        self.assertNotIn("value", json.dumps(rep["spans"][0]))
    def test_date_shift_keeps_intervals(self):
        clean, _ = health.deidentify("Seen 2025-03-14 and 2025-03-24.", date_shift_days=100)
        self.assertIn("[DATE 2025-06-22]", clean); self.assertIn("[DATE 2025-07-02]", clean)
    def test_k_anonymity_improves_with_generalisation(self):
        rows = health.synthetic_cohort(); qis = ["age", "sex", "region"]
        self.assertEqual(health.k_anonymity(rows, qis), 1)
        g = health.generalise(rows, age_band=60, region_map={r: "all regions" for r in ("North", "South", "East", "West")})
        self.assertGreaterEqual(health.k_anonymity(g, qis), 2)
        self.assertGreaterEqual(health.l_diversity(g, qis, "diagnosis"), 2)
    def test_calculators(self):
        e = health.egfr_ckd_epi_2021(health.creatinine_umol_to_mgdl(812), 67, False); self.assertTrue(5.0 < e < 6.5)
        self.assertAlmostEqual(health.egfr_ckd_epi_2021(1.0, 50, True), 68.6, delta=0.5)
        self.assertAlmostEqual(health.urr(25.0, 8.0), 68.0); self.assertAlmostEqual(health.ktv_daugirdas2(25.0, 8.0, 4.0, 2.5, 68.0), 1.351, delta=0.002)
    def test_record_validation_and_scoring(self):
        good = {"learner": "L-017", "case_id": "x", "problem_representation": "Anuric man on haemodialysis with hyperkalaemia after a missed session",
                "differentials": [{"diagnosis": "hyperkalaemia"}], "information_sought": ["ECG"], "decisions": [{"decision": "urgent dialysis", "rationale": "potassium 6.4"}],
                "uncertainty": "medicine history incomplete"}
        self.assertEqual(health.validate_record(good), []); self.assertTrue(health.validate_record({"learner": 3}))
        self.assertGreaterEqual(health.score_record(good)["score"], 0.6)
    def test_grounding_flags_an_invented_number(self):
        self.assertEqual(health.grounding("Potassium 6.4 and sodium 131", health.CASE_TEXT), ["131"])
    def test_rule_provider_is_keyless(self):
        p = health.RuleProvider(); self.assertIn("?", p.complete([]))
    def test_endpoint_provider_against_a_local_stand_in(self):
        class H(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                n = int(self.headers["Content-Length"]); body = json.loads(self.rfile.read(n))
                out = json.dumps({"choices": [{"message": {"content": "Which test first? (%d messages)" % len(body["messages"])}}]}).encode()
                self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(out)
            def log_message(self, *a): pass
        srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            p = health.EndpointProvider("http://127.0.0.1:%d/v1" % srv.server_port, "stand-in")
            self.assertIn("2 messages", p.complete(health.tutor_messages(health.CASE_TEXT, "hyperkalaemia")))
        finally:
            srv.shutdown()
    def test_fhir_bundle_shape(self):
        b = health.fhir_bundle(); self.assertEqual(b["resourceType"], "Bundle")
        self.assertTrue(all(e["fullUrl"].startswith("urn:uuid:") for e in b["entry"]))
        self.assertNotIn("Adeyemi", json.dumps(b))

class RefCheck(unittest.TestCase):
    def test_states_against_a_stand_in(self):
        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if "/works/10.1/good" in self.path: m = {"title": ["A true title"], "issued": {"date-parts": [[2020]]}}
                elif "/works/10.1/bad" in self.path: m = {"title": ["Something else"], "issued": {"date-parts": [[2020]]}}
                elif self.path.startswith("/works?"): m = {"items": [{"title": ["Guidance on things"], "DOI": "10.9/x"}]}
                else: self.send_response(404); self.end_headers(); return
                out = json.dumps({"message": m}).encode(); self.send_response(200); self.end_headers(); self.wfile.write(out)
            def log_message(self, *a): pass
        srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            refcheck.CROSSREF = "http://127.0.0.1:%d" % srv.server_port
            self.assertEqual(refcheck.check({"id": "a", "doi": "10.1/good", "title": "A true title", "year": 2020})["state"], "verified")
            self.assertEqual(refcheck.check({"id": "b", "doi": "10.1/bad", "title": "A true title", "year": 2020})["state"], "open")
            self.assertEqual(refcheck.check({"id": "c", "kind": "guideline", "title": "Guidance on things"})["state"], "verified")
            self.assertEqual(refcheck.check({"id": "d", "doi": "10.1/missing", "title": "x"})["state"], "open")
        finally:
            srv.shutdown()

if __name__ == "__main__":
    unittest.main()
