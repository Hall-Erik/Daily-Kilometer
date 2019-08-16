import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { RunListComponent } from './runs/run-list/run-list.component';

import { RegisterComponent } from './users/register/register.component';
import { LoginComponent } from './users/login/login.component';
import { ForgotPasswordComponent } from './users/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './users/reset-password/reset-password.component';
import { AccountComponent } from './users/account/account.component';

const routes: Routes = [
  {path: '', pathMatch: 'full', redirectTo: 'index'},
  {path: 'index', component: RunListComponent},
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
