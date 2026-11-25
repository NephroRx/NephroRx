import { calculateDoseForDrug, calculateAllDoses, getDrugById, DRUG_CONFIGS } from "./dosing";

const reference = { age: 40, sex: "male", weightKg: 70, serumCreatinine: 1.0, tkvMeasured: 340 };

test("expected TKV equals the male base value at age 40 and 70 kg", () => {
  const r = calculateDoseForDrug(getDrugById("vancomycin"), reference);
  expect(r.tkvExpected).toBeCloseTo(340);
  expect(r.kidneyRatio).toBeCloseTo(1.0);
});

test("TKV-adjusted dose scales the weight-based dose by the kidney ratio", () => {
  const r = calculateDoseForDrug(getDrugById("vancomycin"), { ...reference, tkvMeasured: 170 });
  expect(r.doseNormalMg).toBeCloseTo(70 * 17.5);
  expect(r.kidneyRatio).toBeCloseTo(0.5);
  expect(r.doseTkvMg).toBeCloseTo(70 * 17.5 * 0.5);
});

test("age above 40 lowers expected TKV by 1% per year", () => {
  const r = calculateDoseForDrug(getDrugById("amikacin"), { ...reference, age: 60 });
  expect(r.tkvExpected).toBeCloseTo(340 * 0.8);
});

test("every configured drug produces a finite dose", () => {
  const all = calculateAllDoses(reference);
  expect(all).toHaveLength(DRUG_CONFIGS.length);
  all.forEach((r) => expect(Number.isFinite(r.doseTkvMg)).toBe(true));
});

test("drug lookup is case-insensitive by id or display name", () => {
  expect(getDrugById("Ketamine").id).toBe("ketamine");
  expect(getDrugById("ENOXAPARIN").id).toBe("enoxaparin");
});
