import { Component, OnInit, Input } from '@angular/core';

import { UserService } from '../../services/user.service';
import { User } from '../../models/user';
import { Run } from '../../models/run';

@Component({
  selector: 'app-run-pill',
  templateUrl: './run-pill.component.html',
  styleUrls: ['./run-pill.component.css']
})
export class RunPillComponent implements OnInit {
  @Input() run: Run;
  user: User;

  constructor(private userService: UserService) { }

  ngOnInit() {
    this.user = this.userService.user.getValue();
    this.userService.user.subscribe(user => this.user = user);
  }

}
