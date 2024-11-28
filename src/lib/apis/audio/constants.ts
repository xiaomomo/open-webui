export interface VoicePrompt {
    wavPath: string;
    promptText: string;
    description?: string;  // 可选的描述，帮助理解这组声音的特点
}

export const VOICE_PROMPTS: Record<string, VoicePrompt> = {
    BLIPPI: {
        wavPath: "output/slicer_opt/blippi_sound.mp3_0000832320_0000957760.wav",
        promptText: "Yes, I know the quickest way. We can go to school, the shops, the zoo.",
        description: "Blippi's energetic and educational voice"
    },
    LITTLE_PONY: {
        wavPath: "output/data/littlepony/slicer_opt/littlepony5minter.m4a_0007617920_0007816960.wav",
        promptText: "I don't want to go either. Nope, I've made up my mind. Spike, you can send the letter now. It's okay, girls.",
        description: "Standard male Chinese voice"
    },
    // 可以添加更多声音配置...
};

// 默认声音配置
export const DEFAULT_VOICE_PROMPT = VOICE_PROMPTS.BLIPPI; 
