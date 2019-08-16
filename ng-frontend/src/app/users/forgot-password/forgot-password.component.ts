import { Component } from '@angular/core';
import { Validators, FormBuilder } from '@angular/forms';

import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  sent: boolean = false;
  emailForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]]
  });
  
  get email() { return this.emailForm.get('email'); }

  constructor(private userService: UserService,
              private fb: FormBuilder) { }

  send_request() {
    this.userService.request_reset(this.email.value)
      .subscribe(() => {
        this.sent = true;
      });
  }
}
