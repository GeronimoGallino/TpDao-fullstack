import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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

  private API_URL = 'http://localhost:8000/api/usuarios';
  private backendUsers: User[] = [];


  constructor(private http: HttpClient) {
    const savedUser = localStorage.getItem('user');
    const savedToken = localStorage.getItem('token');

    if (savedUser && savedToken) {
      this.currentUser = JSON.parse(savedUser);
      this.token = savedToken;
    }

    this.getAll().subscribe({
      next: users => {
        this.backendUsers = users;
        console.log('Usuarios cargados para login:', this.backendUsers);
      },
      error: err => console.error('Error cargando usuarios:', err)
    });
  }

  getAll(): Observable<User[]> {
    const res$ = this.http.get<User[]>(this.API_URL);
    res$.subscribe(data => console.log('Datos recibidos:', data));
    return res$;
  }

  createUser(data: User): Observable<any> {
    return this.http.post<any>(this.API_URL, data);
  }

  private readonly USERS = [
    { email: 'admin@test.com', password: '123456', id: 1, role: 'admin' as const },
    { email: 'user@test.com', password: '123456', id: 2, role: 'user' as const },
  ];

  private currentUser: User | null = null;
  private token: string | null = null;
  login(credentials: { email: string; password: string }): Observable<LoginResponse> {

    // SI HAY USUARIOS REALES, VALIDAMOS CON EL BACKEND
    if (this.backendUsers.length > 0) {
      const user = this.backendUsers.find(
        u => u.email === credentials.email && u.password === credentials.password
      );

      if (!user) {
        return throwError(() => ({ error: { detail: 'Credenciales inválidas' } }));
      }

      const token = 'fake-jwt-token-' + Date.now();
      this.token = token;
      this.currentUser = user;

      return of({ token, user }).pipe(delay(500));
    }

    // SI EL BACK NO RESPONDE: usar USERS original (NO toco tu lógica)
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
