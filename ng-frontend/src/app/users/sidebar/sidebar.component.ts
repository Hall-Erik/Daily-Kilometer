import { Component, OnInit } from '@angular/core';

import { UserService } from '../../services/user.service';

import { User } from '../../models/user';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  user: User = this.userService.user.getValue();

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.userService.user.subscribe(user => this.user = user);
    this.userService.get_user().subscribe();
  }
}