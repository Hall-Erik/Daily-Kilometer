import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { NgbModule, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';

import { AlertService } from './services/alert.service';
import { GearService } from './services/gear.service';
import { UserService } from './services/user.service';
import { RunService } from './services/run.service';

import { ApiInterceptor } from './services/api.interceptor';
import { LoginComponent } from './users/login/login.component';
import { RunListComponent } from './runs/run-list/run-list.component';
import { RegisterComponent } from './users/register/register.component';
import { AccountComponent } from './users/account/account.component';
import { ForgotPasswordComponent } from './users/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './users/reset-password/reset-password.component';
import { AlertComponent } from './alert/alert.component';
import { RunPillComponent } from './runs/run-pill/run-pill.component';
import { RunCreateComponent } from './runs/run-create/run-create.component';
import { RunEditComponent } from './runs/run-edit/run-edit.component';
import { RunFormComponent } from './runs/run-form/run-form.component';
import { RunDetailComponent } from './runs/run-detail/run-detail.component';
import { SidebarComponent } from './users/sidebar/sidebar.component';
import { GearListComponent } from './gear/gear-list/gear-list.component';
import { GearCreateComponent } from './gear/gear-create/gear-create.component';
import { GearEditComponent } from './gear/gear-edit/gear-edit.component';
import { GearFormComponent } from './gear/gear-form/gear-form.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MaterialModule } from './material/material.module';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    LoginComponent,
    RunListComponent,
    RegisterComponent,
    AccountComponent,
    ForgotPasswordComponent,
    ResetPasswordComponent,
    AlertComponent,
    RunPillComponent,
    RunCreateComponent,
    RunEditComponent,
    RunFormComponent,
    RunDetailComponent,
    SidebarComponent,
    GearListComponent,
    GearCreateComponent,
    GearEditComponent,
    GearFormComponent
  ],
  imports: [
    MaterialModule,
    BrowserModule,
    FontAwesomeModule,
    AppRoutingModule,
    ReactiveFormsModule,
    NgbModule,
    HttpClientModule,
    HttpClientXsrfModule.withOptions({
      cookieName: 'csrftoken',
      headerName: 'X-CSRFToken'
    }),
    BrowserAnimationsModule
  ],
  providers: [
    AlertService,
    GearService,
    RunService,
    UserService,
    NgbActiveModal,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ApiInterceptor,
      multi: true
    }
  ],
  entryComponents: [
    GearCreateComponent,
    GearEditComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
