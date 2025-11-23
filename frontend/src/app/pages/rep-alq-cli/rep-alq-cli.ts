import { Component, OnInit } from '@angular/core';
import { ClientesService } from '../../core/services/clientes-service';
import { RepAlqCliService } from '../../core/services/rep-alq-cli';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { VehiculosService } from '../../core/services/vehiculos-service';
import { Vehiculo } from '../../core/interfaces/vehiculo';
import { Empleado } from '../../core/interfaces/empleado';
import { EmpleadosService } from '../../core/services/empleados-service';

@Component({
  selector: 'app-rep-alq-cli',
  standalone: true,
  templateUrl: './rep-alq-cli.html',
  styleUrl: './rep-alq-cli.css',
  imports: [CommonModule, FormsModule], 
  providers: [DatePipe]  
})
export class RepAlqCli implements OnInit {

  listaClientes: any[] = [];
  alquileres: any[] = [];
  clienteId: number | any = null;
  listaVehiculos: Vehiculo[] = [];
  listaEmpleados: Empleado[] = [];;
  clienteSeleccionado: boolean = false;

  constructor(
    private clientesService: ClientesService,
    private repAlqCliService: RepAlqCliService
  ) {}

  ngOnInit(): void {
    this.loadClientes();
  }

  loadClientes(): void {
    this.clientesService.getAll().subscribe({
      next: list => this.listaClientes = list || [],
      error: err => console.error(err)
    });
  }

  onClienteChange(): void {
    this.clienteSeleccionado = true;
    if (!this.clienteId) {
      this.alquileres = [];
      return;
    }

    this.repAlqCliService.getByCliente(this.clienteId).subscribe({
      next: data => this.alquileres = data || [],
      error: err => console.error(err)
    });
    console.log('Alquileres cargados:', this.alquileres);
  }
}
