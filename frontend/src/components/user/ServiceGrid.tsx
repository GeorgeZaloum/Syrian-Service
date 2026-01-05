import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MapPin, DollarSign } from 'lucide-react';
import type { Service } from '@/types';

interface ServiceGridProps {
  services: Service[];
  isLoading: boolean;
  onRequestService: (service: Service) => void;
}

export function ServiceGrid({ services, isLoading, onRequestService }: ServiceGridProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <Card key={i} className="p-6 animate-pulse">
            <div className="h-6 bg-gray-200 rounded mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded mb-4"></div>
            <div className="h-10 bg-gray-200 rounded"></div>
          </Card>
        ))}
      </div>
    );
  }

  if (services.length === 0) {
    return (
      <Card className="p-12 text-center">
        <p className="text-muted-foreground text-lg">
          No services found. Try adjusting your search filters.
        </p>
      </Card>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {services.map((service) => (
        <Card key={service.id} className="p-6 flex flex-col hover:shadow-lg transition-shadow">
          <div className="flex-1">
            <h3 className="text-xl font-semibold mb-2">{service.name}</h3>
            <p className="text-muted-foreground mb-4 line-clamp-3">
              {service.description}
            </p>
            
            <div className="space-y-2 mb-4">
              <div className="flex items-center text-sm text-muted-foreground">
                <MapPin className="h-4 w-4 mr-2" />
                <span>{service.location}</span>
              </div>
              <div className="flex items-center text-sm font-semibold text-primary">
                <DollarSign className="h-4 w-4 mr-1" />
                <span>{service.cost}</span>
              </div>
            </div>
          </div>

          <Button 
            onClick={() => onRequestService(service)}
            className="w-full"
          >
            Request Service
          </Button>
        </Card>
      ))}
    </div>
  );
}
