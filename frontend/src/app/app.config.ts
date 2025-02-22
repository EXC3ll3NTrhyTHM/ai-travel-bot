import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { ExtraOptions, provideRouter, withRouterConfig } from '@angular/router';
import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptors  } from '@angular/common/http';
// import { authInterceptor } from './auth.interceptor';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes, withRouterConfig({ scrollPositionRestoration: 'enabled' } as ExtraOptions)),
    provideHttpClient(),
  ]
};
