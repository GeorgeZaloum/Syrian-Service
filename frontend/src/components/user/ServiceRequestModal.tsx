import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import type { Service } from '@/types';

interface ServiceRequestModalProps {
  service: Service | null;
  open: boolean;
  onClose: () => void;
  onSubmit: (serviceId: number, message: string) => void;
  isSubmitting: boolean;
}

export function ServiceRequestModal({
  service,
  open,
  onClose,
  onSubmit,
  isSubmitting,
}: ServiceRequestModalProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = () => {
    if (service) {
      onSubmit(service.id, message);
      setMessage('');
    }
  };

  const handleClose = () => {
    setMessage('');
    onClose();
  };

  if (!service) return null;

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Request Service</DialogTitle>
          <DialogDescription>
            Send a request to the service provider for "{service.name}"
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          <div className="space-y-2">
            <Label>Service</Label>
            <p className="text-sm font-medium">{service.name}</p>
          </div>

          <div className="space-y-2">
            <Label>Location</Label>
            <p className="text-sm text-muted-foreground">{service.location}</p>
          </div>

          <div className="space-y-2">
            <Label>Cost</Label>
            <p className="text-sm font-semibold text-primary">${service.cost}</p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="message">Message (Optional)</Label>
            <Input
              id="message"
              placeholder="Add a message for the provider..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={handleClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} disabled={isSubmitting}>
            {isSubmitting ? 'Sending...' : 'Send Request'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
