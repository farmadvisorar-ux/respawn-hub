// RESPAWN Audio Synthesizer (Web Audio API)
// Ultra-low latency, zero external sound assets required

class AudioManager {
    constructor() {
        this.ctx = null;
        this.muted = localStorage.getItem("respawn_audio_muted") === "true";
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === "suspended") {
            this.ctx.resume();
        }
    }

    toggleMute() {
        this.muted = !this.muted;
        localStorage.setItem("respawn_audio_muted", this.muted);
        return this.muted;
    }

    // Gentle tactile click
    playClick() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(800, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(400, this.ctx.currentTime + 0.04);
        
        gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.04);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.04);
    }

    // Chat message pop
    playPop() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = "triangle";
        osc.frequency.setValueAtTime(440, this.ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(880, this.ctx.currentTime + 0.08);

        gain.gain.setValueAtTime(0.12, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.08);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.08);
    }

    // Dual-tone cyber notification chime
    playNotification() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const freqs = [587.33, 880]; // D5, A5
        freqs.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(freq, now + idx * 0.07);

            gain.gain.setValueAtTime(0.14, now + idx * 0.07);
            gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.07 + 0.18);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + idx * 0.07);
            osc.stop(now + idx * 0.07 + 0.18);
        });
    }

    // Esports Ready Check Buzzer
    playReadyCheck() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        // High-energy 3-tone prompt
        const notes = [440, 554.37, 659.25, 880];
        notes.forEach((note, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "sawtooth";
            osc.frequency.setValueAtTime(note, now + idx * 0.08);

            gain.gain.setValueAtTime(0.15, now + idx * 0.08);
            gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.2);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + idx * 0.08);
            osc.stop(now + idx * 0.08 + 0.2);
        });
    }

    // Squad Victory / Join chord
    playChord() {
        if (this.muted) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const chord = [330, 440, 550, 660];
        chord.forEach(freq => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = "triangle";
            osc.frequency.setValueAtTime(freq, now);

            gain.gain.setValueAtTime(0.08, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 0.35);
        });
    }
}

window.audioManager = new AudioManager();
