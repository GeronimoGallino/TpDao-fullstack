import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { AuthService } from '../../services/auth-service';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  model = {
    email: '',
    password: '',
    remember: false
  };

  showPassword = false;
  loading = false;
  errorMessage = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  toggleShowPassword() {
    this.showPassword = !this.showPassword;
  }

  onSubmit(form: NgForm) {
    if (form.invalid) return;
    this.errorMessage = '';
    this.loading = true;

    this.authService.login(this.model).subscribe({
      next: res => {
        this.loading = false;

        // Guardar token
        localStorage.setItem('token', res.token);

        localStorage.setItem('user', JSON.stringify(res.user))

        // Redirigir al home
        this.router.navigate(['/home']);
      },
      error: err => {
        this.loading = false;
        this.errorMessage = err?.error?.detail || 'Error al iniciar sesión';
      }
    });
  }
}
