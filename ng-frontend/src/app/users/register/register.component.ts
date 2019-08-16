import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, Validators, AbstractControl } from '@angular/forms';

import { UserService } from '../../services/user.service';
import { AlertService } from '../../services/alert.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registerForm = this.fb.group({
    username: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    password1: ['', Validators.required],
    password2: ['', Validators.required],
  }, {validator: this.passwords_match});

  get username() { return this.registerForm.get('username'); }
  get email() { return this.registerForm.get('email'); }
  get password1() { return this.registerForm.get('password1'); }
  get password2() { return this.registerForm.get('password2'); }

  public username_err = '';
  public email_err = '';
  public password1_err = '';
  public password2_err = '';

  constructor(private userService: UserService,
              private alertService: AlertService,
              private router: Router,
              private fb: FormBuilder) { }

  passwords_match(c: AbstractControl) {
    if(c.get('password1').value !== c.get('password2').value) {
      return {invalid: true};
    }
  }

  register() {
    this.userService.register(
      this.username.value, this.email.value,
      this.password1.value, this.password2.value)
      .subscribe(() => {
        this.router.navigate(['login']);
        // alertservice here
      }, (err) => {
        // alertservice here
        if(err.error.username) {
          this.username_err = err.error.username;
          this.username.setErrors({'api': true});
        }
        if(err.error.email) {
          this.email_err = err.error.email;
          this.email.setErrors({'api': true});
        }
        if(err.error.password1) {
          this.password1_err = err.error.password1;
          this.password1.setErrors({'api': true});
        }
        if(err.error.password2) {
          this.password2_err = err.error.password2;
          this.password2.setErrors({'api': true});
        }
      });
  }
}
