import { motion, useScroll, useTransform, useInView } from 'framer-motion';
import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { MapPin, DollarSign, Star, ArrowRight } from 'lucide-react';

interface SampleService {
  id: number;
  name: string;
  provider: string;
  description: string;
  location: string;
  cost: number;
  rating: number;
  category: string;
  image: string;
}

const sampleServices: SampleService[] = [
  {
    id: 1,
    name: 'Professional Plumbing',
    provider: 'John Smith',
    description: 'Expert plumbing services for residential and commercial properties.',
    location: 'New York, NY',
    cost: 75,
    rating: 4.8,
    category: 'Home Services',
    image: '🔧',
  },
  {
    id: 2,
    name: 'Web Development',
    provider: 'Sarah Johnson',
    description: 'Custom website design and development for businesses of all sizes.',
    location: 'San Francisco, CA',
    cost: 150,
    rating: 4.9,
    category: 'Technology',
    image: '💻',
  },
  {
    id: 3,
    name: 'Personal Training',
    provider: 'Mike Davis',
    description: 'One-on-one fitness coaching and personalized workout plans.',
    location: 'Los Angeles, CA',
    cost: 60,
    rating: 4.7,
    category: 'Health & Fitness',
    image: '💪',
  },
  {
    id: 4,
    name: 'Graphic Design',
    provider: 'Emily Chen',
    description: 'Creative design solutions for branding, marketing, and digital media.',
    location: 'Chicago, IL',
    cost: 100,
    rating: 4.9,
    category: 'Creative',
    image: '🎨',
  },
  {
    id: 5,
    name: 'House Cleaning',
    provider: 'Maria Garcia',
    description: 'Thorough and reliable cleaning services for homes and offices.',
    location: 'Miami, FL',
    cost: 50,
    rating: 4.6,
    category: 'Home Services',
    image: '🧹',
  },
  {
    id: 6,
    name: 'Photography',
    provider: 'David Lee',
    description: 'Professional photography for events, portraits, and commercial projects.',
    location: 'Seattle, WA',
    cost: 200,
    rating: 5.0,
    category: 'Creative',
    image: '📸',
  },
];

export const ServicePreview = () => {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start'],
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);
  const opacity = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0, 1, 1, 0]);

  return (
    <section ref={ref} className="py-20 px-4 bg-gradient-to-b from-white to-gray-50 overflow-hidden">
      <motion.div style={{ opacity }} className="container mx-auto max-w-7xl">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Explore Popular Services
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Browse through our diverse marketplace of trusted service providers
          </p>
        </motion.div>

        {/* Services Grid with Parallax */}
        <motion.div style={{ y }} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sampleServices.map((service, index) => (
            <ServiceCard
              key={service.id}
              service={service}
              index={index}
              isInView={isInView}
            />
          ))}
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="text-center mt-16"
        >
          <p className="text-lg text-gray-600 mb-6">
            Ready to explore more services?
          </p>
          <LoginPromptButton />
        </motion.div>
      </motion.div>
    </section>
  );
};

interface ServiceCardProps {
  service: SampleService;
  index: number;
  isInView: boolean;
}

const ServiceCard = ({ service, index, isInView }: ServiceCardProps) => {
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);

  const handleInteraction = () => {
    setShowLoginPrompt(true);
  };

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 50, scale: 0.9 }}
        animate={isInView ? { opacity: 1, y: 0, scale: 1 } : {}}
        transition={{
          duration: 0.5,
          delay: index * 0.1,
        }}
        whileHover={{
          y: -12,
          scale: 1.02,
          transition: { duration: 0.3 },
        }}
      >
        <Card
          className="p-6 h-full border-2 border-gray-100 hover:border-blue-300 hover:shadow-2xl transition-all duration-300 cursor-pointer group"
          onClick={handleInteraction}
        >
          {/* Service Image/Icon */}
          <div className="text-6xl mb-4 group-hover:scale-110 transition-transform duration-300">
            {service.image}
          </div>

          {/* Category Badge */}
          <div className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-full mb-3">
            {service.category}
          </div>

          {/* Service Info */}
          <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
            {service.name}
          </h3>
          <p className="text-sm text-gray-500 mb-3">by {service.provider}</p>
          <p className="text-gray-600 mb-4 line-clamp-2">{service.description}</p>

          {/* Details */}
          <div className="space-y-2 mb-4">
            <div className="flex items-center text-sm text-gray-600">
              <MapPin className="w-4 h-4 mr-2 text-gray-400" />
              {service.location}
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center text-sm font-semibold text-gray-900">
                <DollarSign className="w-4 h-4 mr-1 text-green-600" />
                ${service.cost}/hr
              </div>
              <div className="flex items-center text-sm text-yellow-600">
                <Star className="w-4 h-4 mr-1 fill-current" />
                {service.rating}
              </div>
            </div>
          </div>

          {/* Action Button */}
          <motion.div
            whileHover={{ x: 5 }}
            className="flex items-center text-blue-600 font-semibold group-hover:text-blue-700"
          >
            View Details
            <ArrowRight className="w-4 h-4 ml-2" />
          </motion.div>
        </Card>
      </motion.div>

      {/* Login Prompt Dialog */}
      <LoginPromptDialog
        open={showLoginPrompt}
        onClose={() => setShowLoginPrompt(false)}
      />
    </>
  );
};

const LoginPromptButton = () => {
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);

  return (
    <>
      <Button
        size="lg"
        onClick={() => setShowLoginPrompt(true)}
        className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-6 text-lg rounded-full shadow-lg hover:shadow-xl transition-all"
      >
        Browse All Services
        <ArrowRight className="ml-2 w-5 h-5" />
      </Button>
      <LoginPromptDialog
        open={showLoginPrompt}
        onClose={() => setShowLoginPrompt(false)}
      />
    </>
  );
};

interface LoginPromptDialogProps {
  open: boolean;
  onClose: () => void;
}

const LoginPromptDialog = ({ open, onClose }: LoginPromptDialogProps) => {
  const navigate = useNavigate();

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-2xl">Sign in to Continue</DialogTitle>
          <DialogDescription className="text-base pt-2">
            Create an account or sign in to access full service details and request services from providers.
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-3 mt-4">
          <Button
            size="lg"
            onClick={() => navigate('/register')}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
          >
            Create Account
          </Button>
          <Button
            size="lg"
            variant="outline"
            onClick={() => navigate('/login')}
          >
            Sign In
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
