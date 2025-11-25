import { Routes } from '@angular/router';
import { ClientesComponent } from './pages/clientes/clientes';
import { EmpleadosComponent } from './pages/empleados/empleados';
import { VehiculosComponent } from './pages/vehiculos/vehiculos';
import { NuevoAlquilerComponent } from './pages/nuevo-alquiler/nuevo-alquiler';
import { AlquileresComponent } from './pages/alquileres/alquileres';
import { RepAlqCli } from './pages/rep-alq-cli/rep-alq-cli';
import { RepTopAlq } from './pages/rep-top-alq/rep-top-alq';
import { RepAlqPer } from './pages/rep-alq-per/rep-alq-per';
import { RepFacMen } from './pages/rep-fac-men/rep-fac-men';
import { Login } from './core/components/login/login';
import { Home } from './core/components/home/home';
import { AuthGuard } from './core/services/authguard';
import { MantenimientosComponent } from './pages/mant-nuevo/mant-nuevo';
import { MantenimientosListComponent } from './pages/mant-historial/mant-historial';
import { MantenimientosPendComponent } from './pages/mant-pendiente/mant-pendiente';
import { MultasComponent } from './pages/multas/multas';

export const routes: Routes = [
    { path: '', redirectTo: 'home', pathMatch: 'full' },
    { path: 'home', component: Home, canActivate: [AuthGuard] },
    { path: 'clientes', component: ClientesComponent, canActivate: [AuthGuard] },
    { path: 'empleados', component: EmpleadosComponent, canActivate: [AuthGuard] },
    { path: 'vehiculos', component: VehiculosComponent, canActivate: [AuthGuard] },
    { path: 'alquileres/nuevo', component: NuevoAlquilerComponent, canActivate: [AuthGuard] },
    { path: 'alquileres', component: AlquileresComponent, canActivate: [AuthGuard] },
    { path: 'mantenimientos/nuevo', component: MantenimientosComponent, canActivate: [AuthGuard] },
    { path: 'mantenimientos/historial', component: MantenimientosListComponent, canActivate: [AuthGuard] },
    { path: 'mantenimientos/pendientes', component: MantenimientosPendComponent, canActivate: [AuthGuard] },
    { path: 'multas', component: MultasComponent, canActivate: [AuthGuard] },

    // REPORTES: solo admins pueden acceder
    { path: 'reportes/alquileres', component: RepAlqCli, canActivate: [AuthGuard], data: { role: 'admin' } },
    { path: 'reportes/vehiculos', component: RepTopAlq, canActivate: [AuthGuard], data: { role: 'admin' } },
    { path: 'reportes/periodo', component: RepAlqPer, canActivate: [AuthGuard], data: { role: 'admin' } },
    { path: 'reportes/facturacion', component: RepFacMen, canActivate: [AuthGuard], data: { role: 'admin' } },

    { path: 'login', component: Login },
    { path: '**', redirectTo: 'login', pathMatch: 'full' }
];


