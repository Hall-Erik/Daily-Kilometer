import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RunCreateComponent } from './runs/run-create/run-create.component';
import { RunListComponent } from './runs/run-list/run-list.component';
import { RunDetailComponent } from './runs/run-detail/run-detail.component';
import { RunEditComponent } from './runs/run-edit/run-edit.component';

import { GearListComponent } from './gear/gear-list/gear-list.component';

import { RegisterComponent } from './users/register/register.component';
import { LoginComponent } from './users/login/login.component';
import { ForgotPasswordComponent } from './users/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './users/reset-password/reset-password.component';
import { AccountComponent } from './users/account/account.component';

const routes: Routes = [
  {path: '', pathMatch: 'full', redirectTo: 'index'},
  {path: 'index', component: RunListComponent},
  {path: 'runs/new', component: RunCreateComponent},
  {path: 'runs/:id', component: RunDetailComponent},
  {path: 'runs/:id/edit', component: RunEditComponent},
  {path: 'gear', component: GearListComponent},
  {path: 'register', component: RegisterComponent},
  {path: 'login', component: LoginComponent},
  {path: 'forgot-password', component: ForgotPasswordComponent},
  {path: 'reset/:token', component: ResetPasswordComponent},
  {path: 'account', component: AccountComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
