/**
 * Image optimization utilities
 */

/**
 * Generate srcset for responsive images
 */
export const generateSrcSet = (baseUrl: string, widths: number[]): string => {
  return widths.map(width => `${baseUrl}?w=${width} ${width}w`).join(', ');
};

/**
 * Get optimized image URL with parameters
 */
export const getOptimizedImageUrl = (
  url: string,
  options: {
    width?: number;
    height?: number;
    quality?: number;
    format?: 'webp' | 'avif' | 'jpg' | 'png';
  } = {}
): string => {
  const params = new URLSearchParams();
  
  if (options.width) params.append('w', options.width.toString());
  if (options.height) params.append('h', options.height.toString());
  if (options.quality) params.append('q', options.quality.toString());
  if (options.format) params.append('fm', options.format);
  
  const queryString = params.toString();
  return queryString ? `${url}?${queryString}` : url;
};

/**
 * Lazy load image with intersection observer
 */
export const lazyLoadImage = (img: HTMLImageElement) => {
  const src = img.dataset.src;
  if (!src) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        img.src = src;
        img.removeAttribute('data-src');
        observer.unobserve(img);
      }
    });
  });

  observer.observe(img);
};

/**
 * Preload critical images
 */
export const preloadImage = (url: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve();
    img.onerror = reject;
    img.src = url;
  });
};

/**
 * Preload multiple images
 */
export const preloadImages = async (urls: string[]): Promise<void> => {
  await Promise.all(urls.map(preloadImage));
};
