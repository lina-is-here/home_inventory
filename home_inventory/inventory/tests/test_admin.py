from unittest.mock import MagicMock

import pytest
from django.utils.translation import gettext_lazy as _
from mock_django.query import QuerySetMock

from ..admin import ExpiryDateListFilter, MeasurementAdmin
from ..models import Item, Measurement
from .fixtures import created_measurement


class TestExpiryDateListFilter:
    def test_lookups(self):
        filt = ExpiryDateListFilter(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        assert filt.lookups(MagicMock(), MagicMock()) == (
            ("exp", _("Expired")),
            ("exp_today", _("Expiring today")),
            ("exp_7", _("Expiring in the next 7 days")),
            ("exp_30", _("Expiring in the next 30 days")),
        )

    @pytest.mark.parametrize("param", ["exp", "exp_today", "exp_7", "exp_30"])
    def test_queryset(self, param):
        filt = ExpiryDateListFilter(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        filt.used_parameters = {"expiry_date": param}
        qs = QuerySetMock(Item, "item")
        filt_qs = filt.queryset(MagicMock(), qs)
        assert filt_qs is not qs


class TestMeasurementAdmin:
    def test_get_readonly_fields(self, db, created_measurement):
        ma = MeasurementAdmin(Measurement, MagicMock())
        readonly_fields = ma.get_readonly_fields(MagicMock(), created_measurement)
        assert readonly_fields == ()

        created_measurement.is_default = True
        created_measurement.save()
        readonly_fields = ma.get_readonly_fields(MagicMock(), created_measurement)
        assert readonly_fields == ()

        new_measurement = Measurement.objects.create(name="new")
        readonly_fields = ma.get_readonly_fields(MagicMock(), new_measurement)
        assert readonly_fields == ("is_default",)
