import QuantLib as ql
from unittest import TestCase
from qtk import Controller, Field as F, QuantLibConverter as qlc, Template as T


class TestModels(TestCase):

    def test_hw1f_model(self):
        asof_date = "7/5/2016"
        data = [
            {
                F.FORWARD_RATE.id: 0.01,
                F.ASOF_DATE.id: asof_date,
                F.DISCOUNT_BASIS.id: "30/360",
                F.CURRENCY.id: "USD",
                F.OBJECT_ID.id: "USD.Flat.Curve",
                F.TEMPLATE.id: T.TS_YIELD_FLAT
            },
            {
                F.TEMPLATE.id: T.MODELS_YIELD_HW1F,
                F.ALPHA.id: 0.1,
                F.SIGMA1.id: 0.05,
                F.OBJECT_ID.id: "HW1FModel",
                F.YIELD_CURVE.id: "->USD.Flat.Curve",
                F.CURRENCY.id: "USD"
        }]
        res = Controller(data)
        res.process(asof_date)
        model = res.object("HW1FModel")
        params = list(model.params())
        self.assertListEqual(params, [0.1, 0.05])

    def test_swaption_helpers(self):
        asof_date = "7/5/2016"
        data = [
            {
                F.FORWARD_RATE.id: 0.01,
                F.ASOF_DATE.id: asof_date,
                F.DISCOUNT_BASIS.id: "30/360",
                F.CURRENCY.id: "USD",
                F.OBJECT_ID.id: "USD.Flat.Curve",
                F.TEMPLATE.id: T.TS_YIELD_FLAT
            },
            {
                F.TEMPLATE.id: T.INDEXES_IBOR_USDLIBOR.id,
                F.TENOR.id: "3M",
                F.OBJECT_ID.id: "USDLibor3M",
                F.YIELD_CURVE.id: "->USD.Flat.Curve"
            },
            {
                F.TEMPLATE.id: T.INST_DERIVATIVE_SWAPTION_HELPER.id,
                F.MATURITY_TENOR.id: "1Y",
                F.UNDERLYING_MATURITY_TENOR.id: "5Y",
                F.DISCOUNT_CURVE.id: "->USD.Flat.Curve",
                F.VOLATILITY.id: 0.15,
                F.OBJECT_ID.id: "SWPN1",
                F.CURRENCY.id: "USD",
                F.INDEX.id: "->USDLibor3M"

            }
        ]
        res = Controller(data)
        res.process(asof_date)
        swpn = res.object("SWPN1")