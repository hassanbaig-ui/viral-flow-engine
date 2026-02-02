import { Composition } from 'remotion';
import { ViralComposition } from './ViralComposition';
import clipConfig from './clip_config.json';
import React from 'react';

export const RemotionRoot: React.FC = () => {
    return (
        <>
            {clipConfig.map((clip, index) => (
                <Composition
                    key={index}
                    id={`ViralVideo_${index}`}
                    component={ViralComposition}
                    durationInFrames={(clip.end_time - clip.start_time) * 30}
                    fps={30}
                    width={1080}
                    height={1920}
                    defaultProps={{
                        clipIndex: index,
                        videoUrl: clip.video_url,
                        startTime: clip.start_time,
                        endTime: clip.end_time,
                        title: clip.title,
                        transcript: clip.transcript
                    }}
                />
            ))}
        </>
    );
};

