import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZonelessChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { LocationStrategy, HashLocationStrategy } from '@angular/common'; // <-- ¡VERIFICAR ESTAS IMPORTACIONES!
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(),
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    
    // 1. SOLO proveer el router con tus rutas
    provideRouter(routes), 
    
    provideClientHydration(withEventReplay()),
    
    // 2. Usar el provider para la Estrategia Hash
    // Esto asegura que la URL funcione como localhost:4200/#/clientes
    { provide: LocationStrategy, useClass: HashLocationStrategy } 
  ]
};