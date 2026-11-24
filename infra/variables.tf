variable "project_name" {
  description = "Nombre base para etiquetar e identificar los recursos de ScentCraft"
  type        = string
  default     = "scentcraft"
}

variable "location" {
  description = "Region de Azure habilitada en la suscripcion de estudiante"
  type        = string
  default     = "spaincentral"
}

variable "vm_size" {
  description = "Tamano economico de la maquina virtual para pruebas"
  type        = string
  default     = "Standard_B2ats_v2"
}

variable "admin_username" {
  description = "Usuario administrador de la VM Ubuntu"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Ruta local a la clave publica SSH"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}
