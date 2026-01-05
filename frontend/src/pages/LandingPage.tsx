import { HeroSection } from '@/components/landing/HeroSection';
import { FeaturesGrid } from '@/components/landing/FeaturesGrid';
import { ServicePreview } from '@/components/landing/ServicePreview';
import { Footer } from '@/components/landing/Footer';

export const LandingPage = () => {
  return (
    <div className="min-h-screen">
      <HeroSection />
      <FeaturesGrid />
      <ServicePreview />
      <Footer />
    </div>
  );
};
