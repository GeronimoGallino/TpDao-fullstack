import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';
import { delay } from 'rxjs/operators';
import { User } from '../interfaces/user';

export interface LoginResponse {
  token: string;
  user: User;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly USERS = [
    { email: 'admin@test.com', password: '123456', id: 1, role: 'admin' as const },
    { email: 'user@test.com', password: '123456', id: 2, role: 'user' as const },
  ];

  private currentUser: User | null = null;
  private token: string | null = null;

  constructor() {
    const savedUser = localStorage.getItem('user');
    const savedToken = localStorage.getItem('token');

    if (savedUser && savedToken) {
      this.currentUser = JSON.parse(savedUser);
      this.token = savedToken;
    }
  }

  login(credentials: { email: string; password: string }): Observable<LoginResponse> {
    const user = this.USERS.find(
      u => u.email === credentials.email && u.password === credentials.password
    );

    if (!user) {
      return throwError(() => ({ error: { detail: 'Credenciales inválidas' } }));
    }

    const token = 'fake-jwt-token-' + Date.now();
    this.token = token;
    this.currentUser = { id: user.id, email: user.email, role: user.role };

    return of({ token, user: this.currentUser }).pipe(delay(500));
  }

  logout(): void {
    this.currentUser = null;
    this.token = null;
  }

  getCurrentUser(): User | null {
    return this.currentUser;
  }

  getToken(): string | null {
    return this.token;
  }

  isAuthenticated(): boolean {
    return this.token !== null;
  }

  hasRole(role: 'admin' | 'user'): boolean {
    return this.currentUser?.role === role;
  }
}