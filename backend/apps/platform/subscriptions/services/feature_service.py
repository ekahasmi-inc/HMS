from apps.platform.subscriptions.models import Subscription


class FeatureService:
    """
    Centralized feature evaluation service.

    All platform modules must use this service instead of
    querying SubscriptionFeature directly.
    """

    @staticmethod
    def get_active_subscription(tenant):
        """
        Returns the tenant's active subscription.
        """

        return (
            Subscription.objects
            .select_related("plan")
            .filter(
                tenant=tenant,
                status=Subscription.Status.ACTIVE,
            )
            .first()
        )

    @staticmethod
    def has_feature(tenant, feature_code):
        """
        Returns True if the tenant has an enabled feature.
        """

        subscription = FeatureService.get_active_subscription(tenant)

        if subscription is None:
            return False

        return subscription.features.filter(
            feature__code=feature_code,
            is_enabled=True,
            feature__is_active=True,
        ).exists()

    @staticmethod
    def get_usage_limit(tenant, feature_code):
        """
        Returns the configured usage limit.
        """

        subscription = FeatureService.get_active_subscription(tenant)

        if subscription is None:
            return None

        feature = subscription.features.filter(
            feature__code=feature_code,
            is_enabled=True,
        ).first()

        if feature is None:
            return None

        return feature.usage_limit  

    @staticmethod
    def get_override(tenant, feature_code):
        """
        Returns the configured override value.
        """

        subscription = FeatureService.get_active_subscription(tenant)

        if subscription is None:
            return None

        feature = subscription.features.filter(
            feature__code=feature_code,
            is_enabled=True,
        ).first()

        if feature is None:
            return None
    
        return feature.override_value