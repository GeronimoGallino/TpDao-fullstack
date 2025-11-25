import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AuthService } from '../services/auth-service';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthService, private router: Router) { }

  canActivate(route: ActivatedRouteSnapshot): boolean {
    // Verifica si está logueado
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return false;
    }


    // Verifica rol si la ruta lo requiere
    const expectedRole = route.data['role'] as 'admin' | 'user' | undefined;
    if (expectedRole && !this.authService.hasRole(expectedRole)) {
      alert('Usted no tiene los permisos para ingresar a este componente.')
      this.router.navigate(['/home']);
      return false;
    }

    return true;


  }
}
