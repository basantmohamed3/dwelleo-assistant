# Integrations and CRM Connections

Dwelleo integrates with popular CRM systems, communication tools, and accounting platforms to fit into your existing workflow.

## Supported CRM Integrations

### Native Integrations

The following CRMs have native, two-way sync with Dwelleo. Leads, contacts, and listings sync automatically every 5 minutes.

- **Salesforce** — available on Professional and Enterprise plans.
- **HubSpot** — available on all paid plans.
- **Zoho CRM** — available on Professional and Enterprise plans.
- **Odoo CRM** — available on Enterprise plans. Custom field mapping supported.
- **Bitrix24** — available on Professional and Enterprise plans.

### Setting Up a CRM Integration

1. Go to Settings > Integrations.
2. Select your CRM from the list and click "Connect."
3. Authorize Dwelleo via OAuth (you'll be redirected to your CRM's login).
4. Choose which objects to sync: leads only, contacts only, or both.
5. Map Dwelleo fields to your CRM fields. Default mappings are pre-filled.
6. Click "Test Sync" to confirm a sample record syncs correctly.
7. Enable "Auto Sync" to start continuous syncing.

## Communication Integrations

- **WhatsApp Business** — receive lead inquiries directly to WhatsApp. Available on all paid plans.
- **Slack** — notifications for new leads, listing approvals, and price changes. Available on Professional and Enterprise plans.
- **Email** — SMTP integration with custom domains for branded lead emails. Enterprise only.

## Accounting and Finance

- **QuickBooks Online** — sync invoices and commission payments. Professional and Enterprise plans.
- **Xero** — similar to QuickBooks. Professional and Enterprise plans.
- **Zoho Books** — bundled with Zoho CRM integration.

## API Access

Enterprise customers receive full API access for custom integrations. The API supports REST and GraphQL, with webhooks for real-time event notifications. Rate limits: 1,000 requests/minute per API key. Documentation available at developers.dwelleo.com.

## Webhooks

Configure webhooks at Settings > Integrations > Webhooks. Supported events include: listing.created, listing.approved, listing.price_changed, lead.received, subscription.changed, and payment.failed. Webhook payloads are signed with HMAC-SHA256 for verification.

## Custom Integrations

For integrations not listed, Enterprise customers can request custom development through their account manager. Typical custom integration timelines are 4–8 weeks depending on complexity.

## Troubleshooting Sync Issues

If a CRM sync stops working: verify the OAuth token hasn't expired (re-authorize in Settings), check the sync log for specific errors, and confirm field mappings haven't been removed in your CRM. Contact support if errors persist for more than 24 hours.
