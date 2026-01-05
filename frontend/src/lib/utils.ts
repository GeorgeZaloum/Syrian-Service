import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
import { toast } from "@/hooks/use-toast"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Toast notification utilities
export const showToast = {
  success: (title: string, description?: string) => {
    toast({
      title,
      description,
      variant: "default",
      className: "border-success bg-success/10",
    });
  },
  error: (title: string, description?: string) => {
    toast({
      title,
      description,
      variant: "destructive",
    });
  },
  info: (title: string, description?: string) => {
    toast({
      title,
      description,
      variant: "default",
    });
  },
  warning: (title: string, description?: string) => {
    toast({
      title,
      description,
      variant: "default",
      className: "border-warning bg-warning/10",
    });
  },
};
