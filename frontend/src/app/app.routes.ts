import { Routes } from '@angular/router';
import { ClientesComponent } from './pages/clientes/clientes';
import { EmpleadosComponent } from './pages/empleados/empleados';
import { VehiculosComponent } from './pages/vehiculos/vehiculos';   
import { NuevoAlquilerComponent } from './pages/nuevo-alquiler/nuevo-alquiler';
import { AlquileresComponent } from './pages/alquileres/alquileres';
import { RepAlqCli } from './pages/rep-alq-cli/rep-alq-cli';
import { RepTopAlq } from './pages/rep-top-alq/rep-top-alq';

export const routes: Routes = [
    {
        path: "clientes",
        component: ClientesComponent
    },
    {       
        path: "empleados",
        component: EmpleadosComponent
    },
    {
        path: "vehiculos",
        component: VehiculosComponent
    },
    {
        path: "alquileres/nuevo",
        component: NuevoAlquilerComponent
    },
    {
        path: "alquileres",
        component: AlquileresComponent
    },
    {
        path: "reportes/alquileres",
        component: RepAlqCli
    },
    {
        path: "reportes/vehiculos",
        component: RepTopAlq
    }
];
