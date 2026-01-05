import { useState, useEffect } from 'react';
import { Search, MapPin, DollarSign } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Card } from '@/components/ui/card';
import type { ServiceSearchParams } from '@/types';

interface ServiceSearchPanelProps {
  onSearchChange: (params: ServiceSearchParams) => void;
}

export function ServiceSearchPanel({ onSearchChange }: ServiceSearchPanelProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [location, setLocation] = useState('');
  const [costRange, setCostRange] = useState<[number, number]>([0, 1000]);

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      const params: ServiceSearchParams = {
        search: searchTerm || undefined,
        location: location || undefined,
        min_cost: costRange[0] > 0 ? costRange[0] : undefined,
        max_cost: costRange[1] < 1000 ? costRange[1] : undefined,
      };
      onSearchChange(params);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchTerm, location, costRange, onSearchChange]);

  return (
    <Card className="p-6 space-y-6">
      <div>
        <h2 className="text-2xl font-bold mb-4">Search Services</h2>
      </div>

      {/* Search Input */}
      <div className="space-y-2">
        <Label htmlFor="search">Search</Label>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            id="search"
            type="text"
            placeholder="Search for services..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* Location Filter */}
      <div className="space-y-2">
        <Label htmlFor="location">Location</Label>
        <div className="relative">
          <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            id="location"
            type="text"
            placeholder="Enter location..."
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      {/* Cost Range Filter */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <Label>Cost Range</Label>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <DollarSign className="h-4 w-4" />
            <span>
              ${costRange[0]} - ${costRange[1] === 1000 ? '1000+' : costRange[1]}
            </span>
          </div>
        </div>
        <Slider
          min={0}
          max={1000}
          step={10}
          value={costRange}
          onValueChange={(value) => setCostRange(value as [number, number])}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>$0</span>
          <span>$1000+</span>
        </div>
      </div>
    </Card>
  );
}
