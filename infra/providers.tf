terraform {
  required_version = ">= 1.5.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-scentcraft-tfstate"
    storage_account_name = "stscentcraftkaito2026"
    container_name       = "tfstate"
    key                  = "scentcraft.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  subscription_id = "2bb1447e-2ea8-4baa-b9f1-add078c7b033"
}
