import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AlertService } from '../services/alert.service';
import { UserService } from '../services/user.service';
import { User } from '../models/user';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  user: User;

  constructor(private userService: UserService,
              private alertService: AlertService,
              private router: Router) { }

  ngOnInit() {
    this.user = this.userService.user.getValue();
    this.userService.user.subscribe(user => this.user = user);
    this.userService.get_user().subscribe();
  }

  logout() {
    this.userService.logout().subscribe();
    this.router.navigate(['']);
    this.alertService.success("Log out successful.");
  }
}
