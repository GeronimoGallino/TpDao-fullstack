import { CommonModule, DatePipe } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RepTopAlqService } from '../../core/services/rep-top-alq';

@Component({
  selector: 'app-rep-top-alq',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  providers: [DatePipe],
  templateUrl: './rep-top-alq.html',
  styleUrl: './rep-top-alq.css'
})
export class RepTopAlq {
  listaClientes: any[] = [];
  alquileres: any[] = [];
  cantidad: number | any = null;
  clienteSeleccionado: boolean = false;

  constructor(
    private repTopAlq: RepTopAlqService
  ) {}

  ngOnInit(): void {
  }

  onCantidadChange(): void {
    this.clienteSeleccionado = true;

    this.repTopAlq.getTopAlquileres(this.cantidad).subscribe({
      next: data => this.alquileres = data || [],
      error: err => console.error(err)
    });
    console.log('Alquileres cargados:', this.alquileres);
  }
}