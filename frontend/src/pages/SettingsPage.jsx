import { Card } from '../components/ui/Card'
import { CheckboxField, InputField, SelectField, TextAreaField } from '../components/forms/FormFields'
import { Button } from '../components/ui/Button'

export function SettingsPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Settings</h2>
      <Card title="Profile">
        <div className="grid gap-4 md:grid-cols-2">
          <InputField label="First Name" defaultValue="Admin" />
          <InputField label="Last Name" defaultValue="User" />
        </div>
        <SelectField
          label="Role"
          options={[
            { label: 'Admin', value: 'admin' },
            { label: 'Environmental Officer', value: 'environmental_officer' },
            { label: 'Field Operator', value: 'field_operator' },
            { label: 'Cleanup Team', value: 'cleanup_team' },
          ]}
          defaultValue="admin"
        />
        <TextAreaField label="Notes" rows={3} placeholder="Add operational notes..." />
        <CheckboxField label="Enable email notifications" defaultChecked />
        <Button>Save Settings</Button>
      </Card>
    </div>
  )
}
