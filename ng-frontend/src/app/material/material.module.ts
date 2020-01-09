import { NgModule } from '@angular/core';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button'; 
import { MatMenuModule } from '@angular/material/menu'; 
import { MatDividerModule } from '@angular/material/divider'; 
import { MatIconModule } from '@angular/material/icon'; 

const material = [
  MatToolbarModule,
  MatButtonModule,
  MatMenuModule,
  MatDividerModule,
  MatIconModule
];

@NgModule({
  imports: [material],
  exports: [material]
})
export class MaterialModule { }
