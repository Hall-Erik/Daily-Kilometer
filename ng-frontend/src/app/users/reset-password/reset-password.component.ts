import { Component, OnInit } from '@angular/core';
import { FormBuilder, AbstractControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

import { UserService } from '../../services/user.service';
import { AlertService } from '../../services/alert.service';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent implements OnInit {
  resetForm = this.fb.group({
    token: '',
    password1: ['', Validators.required],
    password2: ['', Validators.required]
  }, {validator: this.passwords_match});

  get token() { return this.resetForm.get('token'); }
  get password1() { return this.resetForm.get('password1'); }
  get password2() { return this.resetForm.get('password2'); }

  tokenStatus: Status = Status.LOADING;

  constructor(private alertService: AlertService,
              private userService: UserService,
              private fb: FormBuilder,
              private router: Router,
              private route: ActivatedRoute) { }

  ngOnInit() {
    let token = this.route.snapshot.paramMap.get('token');
    this.token.setValue(token);
    // TODO: validate token
    this.tokenStatus = Status.VALID;
  }

  token_loading() { return this.tokenStatus == Status.LOADING; }
  token_valid() { return this.tokenStatus == Status.VALID; }
  token_notfound() { return this.tokenStatus == Status.NOT_FOUND; }
  token_expired() { return this.tokenStatus == Status.EXPIRED; }

  passwords_match(c: AbstractControl) {
    if (c.get('password1').value !== c.get('password2').value) {
      return {invalid: true};
    }
  }

  reset_password() {
    this.userService.reset_password(this.token.value, this.password1.value)
      .subscribe(() => {
        this.router.navigate(['login']);
        //alert service here
      })
  }
}

export enum Status {
  LOADING,
  NOT_FOUND,
  EXPIRED,
  VALID
}