import { Component, OnInit } from '@angular/core';

import { UserService } from './services/user.service';
import { User } from './models/user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  user: User;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.user = this.userService.user.getValue();
    this.userService.user.subscribe(user => this.user = user);
    this.userService.get_user().subscribe();
  }
}
