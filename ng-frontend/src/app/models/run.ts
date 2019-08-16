import { Gear } from './gear';
import { User } from './user';

export class Run {
    pk: number;
    run_date: string;
    distance: number;
    units: string;
    duration: string;
    description: string;
    run_type: string;
    gear: Gear;
    user: User;

    public constructor(init?: Partial<Run>) {
        Object.assign(this, init);
    }
}