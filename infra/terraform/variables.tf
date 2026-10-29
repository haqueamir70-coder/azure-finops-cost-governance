variable "subscription_id" {
  description = "Azure subscription ID for this lab. Keep tfvars out of version control."
  type        = string
  sensitive   = true
}

variable "budget_name" {
  description = "Name for the subscription budget."
  type        = string
  default     = "finops-monthly-budget"
}

variable "budget_amount" {
  description = "Monthly budget amount in the billing currency."
  type        = number
  default     = 1000

  validation {
    condition     = var.budget_amount > 0
    error_message = "budget_amount must be greater than zero."
  }
}

variable "budget_start_date" {
  description = "First day of the budget start month in RFC3339 format, e.g. 2026-10-01T00:00:00Z."
  type        = string
}

variable "budget_end_date" {
  description = "Budget end date in RFC3339 format, e.g. 2027-10-01T00:00:00Z."
  type        = string
}

variable "notification_email" {
  description = "Email address for budget threshold notifications."
  type        = string
}

variable "threshold_percentages" {
  description = "Budget thresholds as percentages from 1 to 100."
  type        = list(number)
  default     = [50, 80, 100]

  validation {
    condition     = length(var.threshold_percentages) > 0 && alltrue([for value in var.threshold_percentages : value >= 1 && value <= 100])
    error_message = "Each budget threshold must be between 1 and 100."
  }
}
