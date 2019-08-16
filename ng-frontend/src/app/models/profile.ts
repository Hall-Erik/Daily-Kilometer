export class Profile {
    pk: number;
    location: string;
    gravatar_url: string;
    latest_shoe_miles: number;
    week_miles: number;
    total_miles: number;

    public constructor(init?: Partial<Profile>) {
        Object.assign(this, init);
    }
}