# Boom CRM Extension (Odoo 18)

Extiende `crm.lead` con campos de categorización, instalación, soporte y flujo de aprobación con *chatter* y botón de acción.

## Funcionalidades
- Nuevos campos en `crm.lead`:
  - `x_lead_category` (selection): residencial, empresarial, gubernamental
  - `x_delivery_deadline` (date)
  - `x_approved_by` (many2one a res.users)
  - `x_approved_date` (date)
  - `x_duration_since_approved` (compute int, readonly)
  - `x_installation_required` (boolean)
  - `x_installation_date` (date)
  - `x_contract_reference` (char)
  - `x_support_required` (boolean)
- Botón **Aprobar Lead**:
  - Asigna usuario actual en `x_approved_by`
  - Fija `x_approved_date` y `x_delivery_deadline` a la fecha actual
  - Publica un mensaje en el chatter
- Vista heredada con los campos y el chatter a la derecha.
- Datos demo con 2 registros.

## Instalación
1. Copia la carpeta `boom_crm_extension/` en tu carpeta de addons.
2. Reinicia Odoo (18) y actualiza la lista de aplicaciones.
3. Instala el módulo **Boom CRM Extension**.

## Pruebas rápidas
- Abre cualquier oportunidad de CRM y usa el botón **Aprobar Lead**.
- Verifica que se llenen los campos de aprobación y que se publique una nota en el chatter.
- Carga los demo data instalando el módulo en una BD nueva o activando el modo desarrollador para importar los registros XML.

## Dependencias
- `crm`

## Licencia
LGPL-3