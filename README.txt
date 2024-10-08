By Dylan Tanaka
This Pygame is supposed to be a rough representation of the C-RAM (Counter Rocket, Artilery, Mortar), itself a deriviation of the US Navy's Phalanx CIWS (Close-in Weapons System). It is a self-contained system designed to automatically fire at and destroy any incoming aerial threats. This could include aircaft, missiles and other projectiles. They are often placed in places of importance which risk being attacked. This includes US Military Bases, some US Embassies in foreign countries, and most larger US Navy warships. It consists of a fire-control radar and a 6 barreled 20mm M61 Vulcan Rotary cannon mounted on a fast turning turret mount. The cannon typically has a little less than 1,000 rounds of ammunition, and fires at a rate of 4,500 rounds per minute (75 rounds per second). 

Now, obviously this pygame is just 2D, so this is no simulator.

Upon opening, the program presents a black screen. Incoming projectiles will automatically start periodically coming in, which must be shot down before it reaches the ground (the bottom of the screen).

The gun is located in the middle of the bottom of the screen. Two circles can be seen around the gun; the first, thicker circle indicates the maximum range of the gun, while the second outer, thinner circle indicates the detection range of the radar. The gun detects incoming projectiles within this second circle; once it does, a green box will be placed around the projectile. It will also calculate the exact point to fire at in order for the bullets to interept the target (called the lead), which is represented by a smaller circle connected to the green box via a line. If the algorithm shows that the projectile cannot be successfully intercepted, the lead circle will dissappear, and a "X" will be placed over the projectile. 

The gun by default is set to AUTO mode. In AUTO mode, the gun will automatically fire perfectly at the lead circle. If preferred, the gun can also be set to MANUAL mode, in which you manually control the gun via your mouse.

Although the AUTO mode fires perfectly at the circle, it still may not hit it. This is because the gun has bullet spread, and has a degree of random deviation from where it's supposed to hit. This is accounted for by the gun's high rate of fire; though one bullet is unlikely to hit on its own, by firing a stream of bullets at the projectile, the chance that a bullet hits increases significantly, with the chance of hitting increasing with the amount of bullets fired.

For higher efficiency, in AUTO mode, the gun will only fire a maximum amount of bullets at a specific projectile before it moves on to the next one. This can be changed in-program. The default number for this variable is 150, which is enough to intercept most projectiles. A higher number gives a higher chance of hitting, but means the gun will fire at only one target for longer and will be more vunerable to being overwhelmed by numerous projectiles.

Although there is an ammo expended indicator, there is no ammo limit, so you could fire the gun forever if desired. Keep in mind that the real life gun only has around 1,000 rounds of ammo; how effective would the system be against numerous incoming targets?

Projectiles are fired from the top right corner of the screen to an area near the gun. Every time a projectile is fired, the delay gets slightly lower, though this can be disabled by setting the variable increasing_projectile_rate to False. The delay between incoming projectiles can be altered by changing the variable projectile_base_cooldown. The number corresponds to the number of in-game frames that pass before the next projctile is fired. Keep in mind that the game runs at 75 frames per second. 

Program keybinds:

a: Toggles between AUTO and MANUAL mode for gun firing.
r/f: Increases/decreases burst count for AUTO mode
v: Toggles all indicators (only the actual objects and effects can be seen when indicators are toggled off)

This program is kind of spaghetti code. There's numerous bugs, heavy styling issues, inefficient and unoptimized code, and more. But I simply had extra time on my hands, and decided to make something fun quickly.