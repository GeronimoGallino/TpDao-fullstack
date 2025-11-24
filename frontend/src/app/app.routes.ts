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

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'home',
        pathMatch: 'full'
    },

    {
        path: 'home',
        component: Home,
        canActivate: [AuthGuard]
    },

    {
        path: 'clientes',
        component: ClientesComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'empleados',
        component: EmpleadosComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'vehiculos',
        component: VehiculosComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'alquileres/nuevo',
        component: NuevoAlquilerComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'alquileres',
        component: AlquileresComponent,
        canActivate: [AuthGuard]
    },
    {
        path: 'reportes/alquileres',
        component: RepAlqCli,
        canActivate: [AuthGuard]
    },
    {
        path: 'reportes/vehiculos',
        component: RepTopAlq,
        canActivate: [AuthGuard]
    },
    {
        path: 'reportes/periodo',
        component: RepAlqPer,
        canActivate: [AuthGuard]
    },
    {
        path: 'reportes/facturacion',
        component: RepFacMen,
        canActivate: [AuthGuard]
    },

    {
        path: 'login',
        component: Login
    },

    {
        path: '**',
        redirectTo: 'login',
        pathMatch: 'full'
    }
];

