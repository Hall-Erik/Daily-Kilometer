import { Component, OnInit } from '@angular/core';

import { UserService } from '../services/user.service';
import { User } from '../models/user';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  user: User;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.user = this.userService.user.getValue();
    this.userService.user.subscribe(user => this.user = user);
    this.userService.get_user().subscribe();
  }

  logout() {
    this.userService.logout().subscribe();
  }
}
