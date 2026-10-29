data "azurerm_client_config" "current" {}

resource "azurerm_consumption_budget_subscription" "monthly" {
  name            = var.budget_name
  subscription_id = "/subscriptions/${var.subscription_id}"
  amount          = var.budget_amount
  time_grain      = "Monthly"

  time_period {
    start_date = var.budget_start_date
    end_date   = var.budget_end_date
  }

  dynamic "notification" {
    for_each = toset(var.threshold_percentages)
    content {
      enabled        = true
      threshold      = notification.value
      operator       = "GreaterThan"
      threshold_type = "Actual"

      contact_emails = [var.notification_email]
    }
  }

  lifecycle {
    precondition {
      condition     = data.azurerm_client_config.current.subscription_id == var.subscription_id
      error_message = "The authenticated Azure CLI/service-principal subscription must match var.subscription_id."
    }
  }
}
