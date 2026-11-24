output "resource_group_name" {
  description = "Nombre del grupo de recursos creado"
  value       = azurerm_resource_group.rg.name
}

output "public_ip_address" {
  description = "Dirección IP pública asignada a la VM de ScentCraft"
  value       = azurerm_public_ip.pip.ip_address
}

output "ssh_connection_command" {
  description = "Comando listo para conectarse por SSH a la máquina"
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.pip.ip_address}"
}
