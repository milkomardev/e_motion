from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, CreateView
from .models import SubscriptionPlan
from collections import defaultdict


class PricingView(TemplateView):
    template_name = 'subscriptions/pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_plans = SubscriptionPlan.objects.all().order_by('duration_months', 'attendance_limit')
        regular_grouped_plans = defaultdict(list)
        kids_grouped_plans = defaultdict(list)

        for plan in all_plans:
            if plan.name.startswith("Kids"):
                kids_grouped_plans[plan.duration_months].append(plan)
            else:
                regular_grouped_plans[plan.duration_months].append(plan)

        context['regular_grouped_plans'] = dict(regular_grouped_plans)
        context['kids_grouped_plans'] = dict(kids_grouped_plans)
        return context
