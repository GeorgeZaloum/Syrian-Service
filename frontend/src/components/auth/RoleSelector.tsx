import type { UserRole } from '@/types';
import { Card } from '@/components/ui/card';

interface RoleSelectorProps {
  selectedRole: UserRole | null;
  onRoleSelect: (role: UserRole) => void;
}

export function RoleSelector({ selectedRole, onRoleSelect }: RoleSelectorProps) {
  return (
    <div className="space-y-3">
      <label className="text-sm font-medium">Select Account Type</label>
      <div className="grid grid-cols-2 gap-3">
        <Card
          className={`p-4 cursor-pointer transition-all hover:shadow-md ${
            selectedRole === 'REGULAR'
              ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
              : 'border-gray-200 hover:border-blue-300'
          }`}
          onClick={() => onRoleSelect('REGULAR')}
        >
          <div className="text-center space-y-2">
            <div className="text-2xl">👤</div>
            <div className="font-semibold">Regular User</div>
            <div className="text-xs text-gray-600">
              Search and request services
            </div>
          </div>
        </Card>

        <Card
          className={`p-4 cursor-pointer transition-all hover:shadow-md ${
            selectedRole === 'PROVIDER'
              ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-500'
              : 'border-gray-200 hover:border-blue-300'
          }`}
          onClick={() => onRoleSelect('PROVIDER')}
        >
          <div className="text-center space-y-2">
            <div className="text-2xl">🛠️</div>
            <div className="font-semibold">Service Provider</div>
            <div className="text-xs text-gray-600">
              Offer and manage services
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
