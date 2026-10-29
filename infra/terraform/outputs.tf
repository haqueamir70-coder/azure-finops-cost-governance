output "budget_name" {
  description = "Name of the configured subscription budget."
  value       = azurerm_consumption_budget_subscription.monthly.name
}

output "budget_amount" {
  description = "Monthly budget amount in the configured billing currency."
  value       = azurerm_consumption_budget_subscription.monthly.amount
}

output "budget_scope" {
  description = "Subscription scope for the budget."
  value       = azurerm_consumption_budget_subscription.monthly.subscription_id
}
