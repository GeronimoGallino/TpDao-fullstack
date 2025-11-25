import { Component, OnInit } from '@angular/core';
import { CommonModule, NgIf, NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth-service';
import { EmpleadosService } from '../../core/services/empleados-service';
import { Empleado } from '../../core/interfaces/empleado';
import { User } from '../../core/interfaces/user';
import { forkJoin } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-seguridad',
  templateUrl: './seguridad.html',
  styleUrls: ['./seguridad.css'],
  standalone: true,
  imports: [CommonModule, FormsModule, NgIf, NgFor]
})
export class SeguridadComponent implements OnInit {

  usuarios: User[] = [];
  empleados: Empleado[] = [];

  selectedUsuario: User | null = null;
  isEditing = false;
  errorMessage: string | null = null;

  constructor(
    private authService: AuthService,
    private empleadosService: EmpleadosService,
    private router: Router   // <-- ESTE
  ) { }

  ngOnInit(): void {
    forkJoin({
      usuarios: this.authService.getAll(),
      empleados: this.empleadosService.getAll()
    }).subscribe({
      next: ({ usuarios, empleados }) => {
        this.usuarios = usuarios || [];
        this.empleados = empleados || [];
      },
      error: err => console.error('Error cargando datos iniciales:', err)
    });
  }

  loadUsuarios(): void {
    this.authService.getAll().subscribe({
      next: list => this.usuarios = list || [],
      error: err => console.error('Error cargando usuarios', err)
    });
  }

  loadEmpleados(): void {
    this.empleadosService.getAll().subscribe({
      next: list => this.empleados = list || [],
      error: err => console.error('Error cargando empleados', err)
    });
  }

  getEmpleado(id_empleado: number): Empleado | null {
    return this.empleados.find(e => e.id === id_empleado) || null;
  }

  newUsuario(): void {
    this.selectedUsuario = {
      id: 0,
      email: '',
      password: '',
      role: 'user'
    };
    this.isEditing = false;
    this.errorMessage = null;
  }

  saveUsuario(): void {
    if (!this.selectedUsuario) return;

    this.errorMessage = null;

    this.authService.createUser(this.selectedUsuario).subscribe({
      next: () => {
        this.loadUsuarios();
        this.cancel();
        alert('Usuario creado con éxito.')
        this.router.navigate(['/home']); 
      },
      error: err => {
        console.error('Error creando usuario:', err);
        this.errorMessage = err?.error?.detail || 'Ocurrió un error';
      }
    });
  }


  cancel(): void {
    this.selectedUsuario = null;
    this.isEditing = false;
    this.errorMessage = null;
  }

}
