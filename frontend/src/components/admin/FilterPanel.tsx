import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Filter, X } from 'lucide-react';
import type { AnalyticsFilters } from '@/types';

interface FilterPanelProps {
  onFiltersChange: (filters: AnalyticsFilters) => void;
}

export function FilterPanel({ onFiltersChange }: FilterPanelProps) {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [role, setRole] = useState<string>('');
  const [activityType, setActivityType] = useState<string>('');

  const applyFilters = () => {
    const filters: AnalyticsFilters = {};
    
    if (startDate) filters.start_date = startDate;
    if (endDate) filters.end_date = endDate;
    if (role) filters.role = role;
    if (activityType) filters.activity_type = activityType;

    onFiltersChange(filters);
  };

  const clearFilters = () => {
    setStartDate('');
    setEndDate('');
    setRole('');
    setActivityType('');
    onFiltersChange({});
  };

  const hasActiveFilters = startDate || endDate || role || activityType;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            Filters
          </CardTitle>
          {hasActiveFilters && (
            <Button variant="ghost" size="sm" onClick={clearFilters}>
              <X className="h-4 w-4 mr-2" />
              Clear
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Start Date</label>
            <Input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">End Date</label>
            <Input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">User Role</label>
            <Select value={role || 'all'} onValueChange={(value) => setRole(value === 'all' ? '' : value)}>
              <SelectTrigger>
                <SelectValue placeholder="All roles" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All roles</SelectItem>
                <SelectItem value="REGULAR">Regular User</SelectItem>
                <SelectItem value="PROVIDER">Service Provider</SelectItem>
                <SelectItem value="ADMIN">Admin</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">Activity Type</label>
            <Select value={activityType || 'all'} onValueChange={(value) => setActivityType(value === 'all' ? '' : value)}>
              <SelectTrigger>
                <SelectValue placeholder="All activities" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All activities</SelectItem>
                <SelectItem value="registration">Registration</SelectItem>
                <SelectItem value="service_request">Service Request</SelectItem>
                <SelectItem value="service_created">Service Created</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="mt-4">
          <Button onClick={applyFilters} className="w-full md:w-auto">
            Apply Filters
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
